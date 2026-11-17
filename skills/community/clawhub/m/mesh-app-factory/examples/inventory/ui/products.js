import supplierSelector from './components/supplier_selector.js';
import categorySelector from './components/category_selector.js';

export default {
inject:['tags','service'],
components:{supplierSelector,categorySelector},
data(){return{
  products:[],
  ctrl:{cur:1,max:0,search:''},
  showDialog:false,
  isEdit:false,
  adjForm:{productId:null,productName:'',newStock:0,remark:''},
  showAdjDialog:false,
  opsData:{name:'',productId:null,list:[],total:0,cur:1,max:1},
  showOpsDialog:false,
  form:{id:null,name:'',category:{id:null,name:''},price:0,costPrice:0,stock:0,minStock:10,unit:'件',supplier:{id:null,name:''},remark:''}
}},

created(){
  this.query(1);
},

methods:{
  query(pg){
    this.ctrl.cur=pg;
    var url="/api/product/list?page="+pg+"&pageSize="+this.service.PAGE_SIZE;
    request({method:"GET",url:url},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK) {
        this.products=[];
        this.ctrl.max=0;
        return
      };
      this.products=resp.data.list||[];
      this.ctrl.max=Math.ceil(resp.data.total/this.service.PAGE_SIZE);
    });
  },

  search(){
    if(this.ctrl.search==''){
      return;
    }
    var url="/api/product/search?keyword="+encodeURIComponent(this.ctrl.search);
    request({method:"GET",url:url},this.service.name).then(resp=>{
      this.ctrl.max=1;
      if(resp.code!=RetCode.OK) {
        this.products=[];
        return;
      }
      this.products=resp.data.list||[];
    });
  },

  resetSearch(){
    this.ctrl.search='';
    this.query(1);
  },

  showAdd(){
    this.isEdit=false;
    this.form={id:null,name:'',category:{id:null,name:''},price:0,costPrice:0,stock:0,minStock:10,unit:'件',supplier:{id:null,name:''},remark:''};
    this.showDialog=true;
  },

  //库存调整（盘点）
  showAdjust(row){
    this.adjForm={productId:row.id, productName:row.name, newStock:row.stock, remark:''};
    this.showAdjDialog=true;
  },
  saveAdjust(){
    if(this.adjForm.newStock<0){this.$refs.errMsg.show(this.tags.pleaseInputStock);return;}
    request({method:"POST",url:"/api/product/adjustStock",data:{productId:this.adjForm.productId,newStock:this.adjForm.newStock,remark:this.adjForm.remark}},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK){
        this.$refs.errMsg.showErr(resp.code,resp.info);
        return;
      }
      this.showAdjDialog=false;
      this.query(this.ctrl.cur);
    });
  },

  //库存流水
  showOps(row){
    this.opsData={name:row.name, productId:row.id, list:[], total:0, cur:1, max:1};
    this.showOpsDialog=true;
    this.loadOps(row.id, 1);
  },
  loadOps(productId, pg){
    var url="/api/product/stockOps?productId="+productId+"&page="+pg+"&pageSize=20";
    request({method:"GET",url:url},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK) return;
      var dt=new Date();
      this.opsData.list=(resp.data.list||[]).map(e=>{
        dt.setTime(e.createAt);
        e.createAt=datetime2str(dt);
        e.typeName=this.tags.opType[e.type]||e.type;
        return e;
      });
      this.opsData.total=resp.data.total;
      this.opsData.max=Math.ceil(resp.data.total/20);
      this.opsData.cur=pg;
    });
  },

  editProduct(row){
    this.isEdit=true;
    this.form={
      id:row.id,
      name:row.name,
      category:{id:row.categoryId,name:row.categoryName||''},
      price:row.price,
      costPrice:row.costPrice,
      stock:row.stock,
      minStock:row.minStock,
      unit:row.unit,
      supplier:{id:row.supplierId,name:row.supplierName||''},
      remark:row.remark||''
    };
    this.showDialog=true;
  },

  saveProduct(){
    var data={
      id:this.form.id,
      name:this.form.name,
      category:this.form.category.id,
      price:this.form.price,
      costPrice:this.form.costPrice,
      minStock:this.form.minStock,
      unit:this.form.unit,
      supplier:this.form.supplier.id,
      remark:this.form.remark
    };
    //库存不允许在编辑商品时直接修改，只能通过盘点(adjustStock)或采购/销售单据变更
    if(!this.isEdit){
      data.stock=this.form.stock;
    }
    var url=this.isEdit?'/api/product/update':'/api/product/create';
    var method=this.isEdit?'PUT':"POST";
    request({method:method,url:url,data:data},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK){
        this.$refs.errMsg.showErr(resp.code,resp.info);
        return;
      }
      this.showDialog=false;
      this.query(this.ctrl.max);
    });
  },

  deleteProduct(id){
    request({method:"DELETE",url:"/api/product/delete?id="+id},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK){
        this.$refs.errMsg.showErr(resp.code,resp.info);
        return;
      }
      this.query(this.ctrl.cur);
    });
  }
},

template:`
<q-layout view="lHh lpr lFf" container style="height:100vh">
<q-header elevated class="bg-primary text-white">
  <q-toolbar>
    <q-btn flat icon="arrow_back" @click="$router.push('/home')"></q-btn>
    <q-toolbar-title>{{tags.products}}</q-toolbar-title>
  </q-toolbar>
</q-header>

<q-footer class="bg-white q-pa-md">
  <q-input outlined v-model="ctrl.search" :label="tags.search" dense @keyup.enter="search">
    <template v-slot:append>
      <q-icon v-if="ctrl.search!==''" name="close" @click="resetSearch" class="cursor-pointer"></q-icon>
      <q-icon name="search" @click="search"></q-icon>
    </template>
    <template v-slot:after>
      <q-btn round color="primary" icon="add_circle" @click="showAdd"></q-btn>
    </template>
  </q-input>
</q-footer>

<q-page-container>
<q-page padding>
  <!-- 商品管理区域 -->
  <div class="row items-center q-mb-md">
    <div class="text-h5">{{tags.products}}</div>
    <q-space></q-space>
    <q-btn color="primary" icon="add" :label="tags.addProduct" @click="showAdd"></q-btn>
  </div>

  <!-- 商品列表 -->
  <q-table :rows="products" :columns="[
    {name:'name',label:tags.productName,field:'name'},
    {name:'categoryName',label:tags.category,field:'categoryName'},
    {name:'price',label:tags.price,field:'price'},
    {name:'costPrice',label:tags.costPrice,field:'costPrice'},
    {name:'stock',label:tags.stock,field:'stock'},
    {name:'unit',label:tags.unit,field:'unit'},
    {name:'action',label:tags.operation,field:'action'}
  ]" row-key="id" flat hide-bottom>
    <template v-slot:body-cell-stock="props">
      <q-td :props="props">
        <span :class="{'text-negative':props.row.stock<=props.row.minStock}">{{props.row.stock}}</span>
      </q-td>
    </template>
    <template v-slot:body-cell-action="props">
      <q-td :props="props">
        <q-btn flat dense color="primary" icon="edit" @click="editProduct(props.row)"></q-btn>
        <q-btn flat dense color="orange" icon="tune" @click="showAdjust(props.row)"></q-btn>
        <q-btn flat dense color="teal" icon="history" @click="showOps(props.row)"></q-btn>
        <q-btn flat dense color="negative" icon="delete" @click="deleteProduct(props.row.id)"></q-btn>
      </q-td>
    </template>
  </q-table>

  <!-- 分页 -->
  <div class="row justify-center q-mt-md" v-if="ctrl.max>1">
    <q-pagination v-model="ctrl.cur" :max="ctrl.max" :max-pages="10" @update:model-value="query"></q-pagination>
  </div>

  <!-- 添加/编辑商品对话框 -->
  <q-dialog v-model="showDialog" persistent>
    <q-card style="min-width:500px">
      <q-card-section><div class="text-h6">{{isEdit?tags.editProduct:tags.addProduct}}</div></q-card-section>
      <q-card-section class="q-pt-none">
        <q-input v-model="form.name" :label="tags.productName" outlined dense required></q-input>
        <category-selector v-model="form.category" :serviceName="service.name"
        :label="tags.category" class="q-mt-sm"></category-selector>
        <div class="row q-col-gutter-sm q-mt-sm">
          <div class="col"><q-input v-model.number="form.price" :label="tags.price" type="number" outlined dense></q-input></div>
          <div class="col"><q-input v-model.number="form.costPrice" :label="tags.costPrice" type="number" outlined dense></q-input></div>
        </div>
        <div class="row q-col-gutter-sm q-mt-sm">
          <div class="col"><q-input v-model.number="form.stock" :label="tags.stock" type="number" outlined dense :disable="isEdit"></q-input></div>
          <div class="col"><q-input v-model.number="form.minStock" :label="tags.minStock" type="number" outlined dense></q-input></div>
        </div>
        <q-input v-model="form.unit" :label="tags.unit" outlined dense class="q-mt-sm"></q-input>
        <supplier-selector v-model="form.supplier" :serviceName="service.name"
         :label="tags.supplier" class="q-mt-sm"></supplier-selector>
        <q-input v-model="form.remark" :label="tags.remark" type="textarea" outlined dense class="q-mt-sm"></q-input>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat :label="tags.cancel" color="grey" v-close-popup></q-btn>
        <q-btn unelevated :label="tags.save" color="primary" @click="saveProduct"></q-btn>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <!-- 库存调整对话框 -->
  <q-dialog v-model="showAdjDialog" persistent>
    <q-card style="min-width:400px">
      <q-card-section><div class="text-h6">{{tags.adjustStock}} - {{adjForm.productName}}</div></q-card-section>
      <q-card-section class="q-pt-none">
        <q-input v-model.number="adjForm.newStock" :label="tags.newStock" type="number" outlined dense autofocus></q-input>
        <q-input v-model="adjForm.remark" :label="tags.adjustReason" outlined dense class="q-mt-sm"></q-input>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat :label="tags.cancel" color="grey" v-close-popup></q-btn>
        <q-btn unelevated :label="tags.save" color="primary" @click="saveAdjust"></q-btn>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <!-- 库存流水对话框 -->
  <q-dialog v-model="showOpsDialog" persistent>
    <q-card style="min-width:500px;max-width:700px">
      <q-card-section><div class="text-h6">{{tags.stockOps}} - {{opsData.name}}</div></q-card-section>
      <q-card-section class="q-pt-none">
        <q-table :rows="opsData.list" :columns="[
          {name:'createAt',label:tags.createTime,field:'createAt'},
          {name:'typeName',label:tags.changeType,field:'typeName'},
          {name:'delta',label:tags.quantity,field:'delta'},
          {name:'before',label:tags.beforeStock,field:'before'},
          {name:'after',label:tags.afterStock,field:'after'},
          {name:'creator',label:tags.creator,field:'creator'},
          {name:'remark',label:tags.remark,field:'remark'}
        ]" row-key="createAt" flat dense hide-bottom>
          <template v-slot:body-cell-delta="props">
            <q-td :props="props">
              <span :class="props.row.delta>=0?'text-positive':'text-negative'">{{props.row.delta>=0?'+':''}}{{props.row.delta}}</span>
            </q-td>
          </template>
        </q-table>
        <div class="row justify-center q-mt-sm" v-if="opsData.max>1">
          <q-pagination v-model="opsData.cur" :max="opsData.max" :max-pages="5" @update:model-value="loadOps(opsData.productId,$event)"></q-pagination>
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat :label="tags.close" color="grey" v-close-popup></q-btn>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <component-alert-dialog ref="errMsg"></component-alert-dialog>
</q-page>
</q-page-container>
</q-layout>
`
}
