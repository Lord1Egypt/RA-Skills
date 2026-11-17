export default {
inject:['tags','service'],
data(){return{
  suppliers:[],
  showDialog:false,
  isEdit:false,
  ctrl:{cur:1,max:0,search:''},
  form:{id:null,name:'',contact:'',phone:'',address:'',remark:''}
}},

created(){
  this.query(1);
},

methods:{
  query(pg){
    this.ctrl.cur=pg;
    var url="/api/supplier/list?page="+pg+"&pageSize="+this.service.PAGE_SIZE;
    request({method:"GET",url:url},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK){
        this.suppliers=[];
        this.ctrl.max=0;
        return;
      } 
      this.suppliers=resp.data.list||[];
      this.ctrl.max=Math.ceil(resp.data.total/this.service.PAGE_SIZE);
      if(this.ctrl.cur>this.ctrl.max) {
        this.ctrl.cur=this.ctrl.max;
      }
    });
  },

  resetSearch(){
    this.ctrl.search='';
    this.query(1);
  },
  
  search(){
    if(!this.ctrl.search){
      return;
    }
    var url="/api/supplier/search?keyword="+encodeURIComponent(this.ctrl.search);
    request({method:"GET",url:url},this.service.name).then(resp=>{
      this.ctrl.max=0;
      if(resp.code!=RetCode.OK) {
        this.suppliers=[];
        return;
      }
      this.suppliers=resp.data.list||[];
    });
  },

  showAdd(){
    this.isEdit=false;
    this.form={id:null,name:'',contact:'',phone:'',address:'',remark:''};
    this.showDialog=true;
  },

  editSupplier(row){
    this.isEdit=true;
    this.form={...row};
    this.showDialog=true;
  },

  saveSupplier(){
    var url=this.isEdit?'/api/supplier/update':'/api/supplier/create';
    var method=this.isEdit?'PUT':"POST";
    request({method:method,url:url,data:this.form},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK){
        this.$refs.errMsg.showErr(resp.code,resp.info);
        return;
      }
      this.showDialog=false;
      this.query(this.ctrl.max);
    });
  },

  deleteSupplier(id){
    request({method:"DELETE",url:"/api/supplier/delete?id="+id},this.service.name).then(resp=>{
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
    <q-toolbar-title>{{tags.suppliers}}</q-toolbar-title>
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
  <q-table :rows="suppliers" :columns="[
    {name:'name',label:tags.supplierName,field:'name'},
    {name:'contact',label:tags.contact,field:'contact'},
    {name:'phone',label:tags.phone,field:'phone'},
    {name:'address',label:tags.address,field:'address'},
    {name:'action',label:tags.operation,field:'action'}
  ]" row-key="id" flat hide-bottom>
    <template v-slot:body-cell-action="props">
      <q-td :props="props">
        <q-btn flat dense color="primary" icon="edit" @click="editSupplier(props.row)"></q-btn>
        <q-btn flat dense color="negative" icon="delete" @click="deleteSupplier(props.row.id)"></q-btn>
      </q-td>
    </template>
  </q-table>
  <div class="q-pa-sm flex flex-center" v-if="ctrl.max>1">
    <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
     boundary-numbers="false" @update:model-value="query"></q-pagination>
  </div>
  
  <q-dialog v-model="showDialog" persistent>
    <q-card style="min-width:400px">
      <q-card-section><div class="text-h6">{{isEdit?tags.editSupplier:tags.addSupplier}}</div></q-card-section>
      <q-card-section class="q-pt-none">
        <q-input v-model="form.name" :label="tags.supplierName" outlined dense class="q-mb-sm"></q-input>
        <q-input v-model="form.contact" :label="tags.contact" outlined dense class="q-mb-sm"></q-input>
        <q-input v-model="form.phone" :label="tags.phone" outlined dense class="q-mb-sm"></q-input>
        <q-input v-model="form.address" :label="tags.address" outlined dense class="q-mb-sm" type="textarea"></q-input>
        <q-input v-model="form.remark" :label="tags.remark" outlined dense type="textarea"></q-input>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat :label="tags.cancel" color="grey-7" v-close-popup></q-btn>
        <q-btn unelevated :label="tags.save" color="primary" @click="saveSupplier"></q-btn>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <component-alert-dialog ref="errMsg"></component-alert-dialog>
</q-page>
</q-page-container>
</q-layout>
`
}
