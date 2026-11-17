export default {
inject:['tags','service'],
data(){return{
  categories:[],
  keyword:'',
  showDialog:false,
  isEdit:false,
  form:{id:null,name:'',remark:''}
}},

created(){
  this.loadData();
},

methods:{
  loadData(){
    var url="/api/category/list?page=1&pageSize=100";
    request({method:"GET",url:url},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK) {
       this.categories=[];
       return;
      }
      this.categories=resp.data.list||[];
    });
  },

  search(){
    if(!this.keyword){
      this.loadData();
      return;
    }
    var url="/api/category/search?keyword="+encodeURIComponent(this.keyword);
    request({method:"GET",url:url},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK) return;
      this.categories=resp.data.list||[];
    });
  },

  resetSearch(){
    this.keyword='';
    this.loadData();
  },

  showAdd(){
    this.isEdit=false;
    this.form={id:null,name:'',remark:''};
    this.showDialog=true;
  },

  editCategory(row){
    this.isEdit=true;
    this.form={id:row.id,name:row.name,remark:row.remark||''};
    this.showDialog=true;
  },

  saveCategory(){
    if(!this.form.name){this.$refs.errMsg.showErr(1,this.tags.pleaseInputCategoryName);return;}
    var url=this.isEdit?'/api/category/update':'/api/category/create';
    var method=this.isEdit?'PUT':"POST";
    request({method:method,url:url,data:this.form},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK){
        this.$refs.errMsg.showErr(resp.code,resp.info);
        return;
      }
      this.showDialog=false;
      this.loadData();
    });
  },

  deleteCategory(id){
    request({method:"DELETE",url:"/api/category/delete?id="+id},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK){this.$refs.errMsg.showErr(resp.code,resp.info);return;}
      this.loadData();
    });
  }
},

template:`
<q-layout view="lHh lpr lFf" container style="height:100vh">
<q-header elevated class="bg-primary text-white">
  <q-toolbar>
    <q-btn flat icon="arrow_back" @click="$router.push('/home')"></q-btn>
    <q-toolbar-title>{{tags.categories}}</q-toolbar-title>
  </q-toolbar>
</q-header>

<q-footer class="bg-white q-pa-md">
  <q-input outlined v-model="keyword" :label="tags.search" dense @keyup.enter="search">
    <template v-slot:append>
      <q-icon v-if="keyword!==''" name="close" @click="resetSearch" class="cursor-pointer"></q-icon>
      <q-icon name="search" @click="search"></q-icon>
    </template>
    <template v-slot:after>
      <q-btn round color="primary" icon="add_circle" @click="showAdd"></q-btn>
    </template>
  </q-input>
</q-footer>

<q-page-container>
<q-page padding>
  <q-list separator>
    <q-item v-for="cat in categories" :key="cat.id">
      <q-item-section>
        <q-item-label>{{cat.name}}</q-item-label>
        <q-item-label caption>{{cat.remark||'-'}}</q-item-label>
      </q-item-section>
      <q-item-section side>
        <q-btn flat dense color="primary" icon="edit" @click="editCategory(cat)"></q-btn>
      </q-item-section>
      <q-item-section side>
        <q-btn flat dense color="negative" icon="delete" @click="deleteCategory(cat.id)"></q-btn>
      </q-item-section>
    </q-item>
    <q-item v-if="!categories.length">
      <q-item-section><q-item-label class="text-grey">{{tags.noData}}</q-item-label></q-item-section>
    </q-item>
  </q-list>

  <q-dialog v-model="showDialog" persistent>
    <q-card style="min-width:400px">
      <q-card-section><div class="text-h6">{{isEdit?tags.editCategory:tags.addCategory}}</div></q-card-section>
      <q-card-section class="q-pt-none">
        <q-input v-model="form.name" :label="tags.categoryName" outlined dense required></q-input>
        <q-input v-model="form.remark" :label="tags.remark" type="textarea" outlined dense class="q-mt-sm"></q-input>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat :label="tags.cancel" color="grey-7" v-close-popup></q-btn>
        <q-btn unelevated :label="tags.save" color="primary" @click="saveCategory"></q-btn>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <component-alert-dialog ref="errMsg"></component-alert-dialog>
</q-page>
</q-page-container>
</q-layout>
`
}
