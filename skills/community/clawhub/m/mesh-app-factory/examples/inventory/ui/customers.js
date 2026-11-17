export default {
inject:['tags','service'],
data(){return{
  customers:[],
  ctrl:{cur:1,max:0,search:''},
  showDialog:false,
  isEdit:false,
  form:{id:null,name:'',phone:'',address:'',remark:''}
}},

created(){
  this.query(1);
},

methods:{
  query(pg){
    this.ctrl.cur=pg;
    var url="/api/customer/list?page="+pg+"&pageSize="+this.service.PAGE_SIZE;
    request({method:"GET",url:url},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK||resp.data.total==0){
        this.customers=[];
        this.ctrl.max=0;
        this.ctrl.cur=1;
        return;
      }
      this.customers=resp.data.list||[];
      this.ctrl.max=Math.ceil(resp.data.total/this.service.PAGE_SIZE);
    });
  },
  
  search(){
    if(this.ctrl.search==''){
      return;
    }
    var url="/api/customer/search?keyword="+encodeURIComponent(this.ctrl.search);
    request({method:"GET",url:url},this.service.name).then(resp=>{
      this.ctrl.max=1;
      if(resp.code!=RetCode.OK) {
        this.customers=[];
        return;
      }
      this.customers=resp.data.list||[];
    });
  },
  
  resetSearch(){
    this.ctrl.search='';
    this.query(1);
  },
  
  showAdd(){
    this.isEdit=false;
    this.form={id:null,name:'',phone:'',address:'',remark:''};
    this.showDialog=true;
  },
  
  editCustomer(row){
    this.isEdit=true;
    this.form={...row};
    this.showDialog=true;
  },
  
  saveCustomer(){
    if(!this.form.name){this.$refs.errMsg.showErr(1,this.tags.pleaseInputCustomerName);return;}
    var url=this.isEdit?'/api/customer/update':'/api/customer/create';
    var method=this.isEdit?'PUT':"POST";
    request({method:method,url:url,data:this.form},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK){
        this.$refs.errMsg.showErr(resp.code,resp.info);
        return;
      }
      this.showDialog=false;
      this.query(1);
    });
  },
  
  deleteCustomer(id){
    request({method:"DELETE",url:"/api/customer/delete?id="+id},this.service.name).then(resp=>{
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
    <q-toolbar-title>{{tags.customers}}</q-toolbar-title>
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
  <q-table :rows="customers" :columns="[
    {name:'name',label:tags.customerName,field:'name'},
    {name:'phone',label:tags.phone,field:'phone'},
    {name:'address',label:tags.address,field:'address'},
    {name:'action',label:tags.operation,field:'action'}
  ]" row-key="id" flat hide-bottom>
    <template v-slot:body-cell-action="props">
      <q-td :props="props">
        <q-btn flat dense color="primary" icon="edit" @click="editCustomer(props.row)"></q-btn>
        <q-btn flat dense color="negative" icon="delete" @click="deleteCustomer(props.row.id)"></q-btn>
      </q-td>
    </template>
  </q-table>

  <div class="q-pa-sm flex flex-center" v-if="ctrl.max>1">
    <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10" boundary-numbers="false" @update:model-value="query"></q-pagination>
  </div>

  <q-dialog v-model="showDialog" persistent>
    <q-card style="min-width:400px">
      <q-card-section><div class="text-h6">{{isEdit?tags.editCustomer:tags.addCustomer}}</div></q-card-section>
      <q-card-section class="q-pt-none">
        <q-input v-model="form.name" :label="tags.customerName" outlined dense class="q-mb-sm"></q-input>
        <q-input v-model="form.phone" :label="tags.phone" outlined dense class="q-mb-sm"></q-input>
        <q-input v-model="form.address" :label="tags.address" outlined dense class="q-mb-sm" type="textarea"></q-input>
        <q-input v-model="form.remark" :label="tags.remark" outlined dense type="textarea"></q-input>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat :label="tags.cancel" color="grey-7" v-close-popup></q-btn>
        <q-btn unelevated :label="tags.save" color="primary" @click="saveCustomer"></q-btn>
      </q-card-actions>
    </q-card>
  </q-dialog>
  
  <component-alert-dialog ref="errMsg"></component-alert-dialog>
</q-page>
</q-page-container>
</q-layout>
`
}
